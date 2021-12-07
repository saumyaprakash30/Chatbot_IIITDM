import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageComponent } from './recv-message.component';

describe('RecvMessageComponent', () => {
  let component: RecvMessageComponent;
  let fixture: ComponentFixture<RecvMessageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

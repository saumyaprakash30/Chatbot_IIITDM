import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageTableComponent } from './recv-message-table.component';

describe('RecvMessageTableComponent', () => {
  let component: RecvMessageTableComponent;
  let fixture: ComponentFixture<RecvMessageTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
